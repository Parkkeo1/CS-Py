import math


class MatchAnalysis:

    # Formula Constants
    HLTV_KPR_CONST = 0.658
    HLTV_SURVIVAL_CONST = 0.318
    HLTV_MULTIKILL_CONST = 1.193
    HLTV_DIVIDE_CONST = 2.7

    def __init__(self, round_data_df):
        self.data_frame = round_data_df

        # simple properties
        self.steamid = int(self.data_frame['SteamID'].iloc[-1])  # to keep track of user when sending match data to remote.
        self.start = int(self.data_frame['Time'].iloc[0])
        self.end = int(self.data_frame['Time'].iloc[-1])
        self.round_count = self.data_frame.shape[0]
        self.map_name = self.data_frame['Map'].iloc[-1]

        # overall stats
        self.kills = int(self.data_frame['Kills'].iloc[-1])
        self.assists = int(self.data_frame['Assists'].iloc[-1])
        self.deaths = int(self.data_frame['Deaths'].iloc[-1])
        self.score = int(self.data_frame['Score'].iloc[-1])

        # to-be calculated properties
        self.rating1 = 0
        self.hsr, self.ct_hsr, self.t_hsr = 0, 0, 0
        self.mdc, self.ct_mdc, self.t_mdc = 0, 0, 0
        self.kpr, self.ct_kpr, self.t_kpr = 0, 0, 0
        self.kas, self.ct_kas, self.t_kas = 0, 0, 0
        self.kdr, self.ct_kdr, self.t_kdr = 0, 0, 0
        self.kda, self.ct_kda, self.t_kda = 0, 0, 0
        self.mean_equip, self.ct_mean_equip, self.t_mean_equip = 0, 0, 0

        # Function to calculate all performance metrics
        self.calculate_main()

    def calculate_main(self):
        first_team = self.data_frame['Player Team'].iloc[0]

        ct_data = self.data_frame[self.data_frame['Player Team'] == 'CT']
        t_data = self.data_frame[self.data_frame['Player Team'] == 'T']

        # HSR: Headshot Ratio
        # MDC: Monetary Dependency Coefficient
        # KPR: Kills Per Round
        # KDR, KDA: Kill Death Ratio, Kill+Assist Death Ratio
        # MEAN: Mean Equipment Value

        # Totals
        if not self.data_frame.empty:
            self.rating1 = self.calculate_rating(self.data_frame)
            self.hsr = self.calculate_hsr(self.data_frame)
            self.mdc = self.calculate_mdc(self.data_frame)
            self.kpr = self.calculate_kpr(self.data_frame)
            self.kas = self.calculate_kas(self.data_frame, 0, 0, 0)
            self.kdr, self.kda = self.calculate_kdr_kda(self.data_frame, 0, 0, 0)
            self.mean_equip = int(round(self.data_frame['Current Equip. Value'].mean(skipna=True)))

        # CT
        if not ct_data.empty:
            self.ct_hsr = self.calculate_hsr(ct_data)
            self.ct_mdc = self.calculate_mdc(ct_data)
            self.ct_kpr = self.calculate_kpr(ct_data)

            if first_team == 'CT':
                self.ct_kas = self.calculate_kas(ct_data, 0, 0, 0)
                self.ct_kdr, self.ct_kda = self.calculate_kdr_kda(ct_data, 0, 0, 0)
            else:
                self.ct_kas = self.calculate_kas(ct_data, t_data['Kills'].iloc[-1], t_data['Assists'].iloc[-1],
                                                 t_data['Deaths'].iloc[-1])
                self.ct_kdr, self.ct_kda = self.calculate_kdr_kda(ct_data, t_data['Kills'].iloc[-1],
                                                                  t_data['Assists'].iloc[-1], t_data['Deaths'].iloc[-1])

            self.ct_mean_equip = int(round(ct_data['Current Equip. Value'].mean(skipna=True)))

        # T
        if not t_data.empty:
            self.t_hsr = self.calculate_hsr(t_data)
            self.t_mdc = self.calculate_mdc(t_data)
            self.t_kpr = self.calculate_kpr(t_data)

            if first_team == 'T':
                self.t_kas = self.calculate_kas(t_data, 0, 0, 0)
                self.t_kdr, self.t_kda = self.calculate_kdr_kda(t_data, 0, 0, 0)
            else:
                self.t_kas = self.calculate_kas(t_data, ct_data['Kills'].iloc[-1], ct_data['Assists'].iloc[-1],
                                                ct_data['Deaths'].iloc[-1])
                self.t_kdr, self.t_kda = self.calculate_kdr_kda(t_data, ct_data['Kills'].iloc[-1],
                                                                ct_data['Assists'].iloc[-1], ct_data['Deaths'].iloc[-1])

            self.t_mean_equip = int(round(t_data['Current Equip. Value'].mean(skipna=True)))

    def calculate_rating(self, relevant_data_df):
        # HLTV's Kill Rating Formula
        kill_rating = self.calculate_kpr(relevant_data_df) / MatchAnalysis.HLTV_KPR_CONST

        total_rounds = relevant_data_df.shape[0]
        # HLTV's Survival Rating Formula
        survival_rating = ((total_rounds - relevant_data_df['Deaths'].iloc[-1]) / total_rounds) / MatchAnalysis.HLTV_SURVIVAL_CONST

        multikill_rounds = [0, 0, 0, 0, 0, 0]

        for i in range(total_rounds):
            multikill_rounds[int(relevant_data_df['Round Kills'].iloc[i])] += 1

        # HLTV's MultiKill Rating Formula
        multikill_rating = ((multikill_rounds[1] +
                           (4 * multikill_rounds[2]) +
                           (9 * multikill_rounds[3]) +
                           (16 * multikill_rounds[4]) +
                           (25 * multikill_rounds[5])) / total_rounds) / MatchAnalysis.HLTV_MULTIKILL_CONST

        # HLTV's Rating 1.0 Formula
        combined_rating = (kill_rating + (0.7 * survival_rating) + multikill_rating) / MatchAnalysis.HLTV_DIVIDE_CONST
        return float(round(combined_rating, 2))

    @staticmethod
    def calculate_hsr(relevant_data_df):
        total_kills = relevant_data_df['Round Kills'].sum(skipna=True)
        total_hs_kills = relevant_data_df['Round HS Kills'].sum(skipna=True)

        if total_kills == 0 or total_hs_kills == 0:
            return 0
        else:
            return float(round(total_hs_kills / total_kills, 3))

    @staticmethod
    def calculate_mdc(relevant_data_df):
        mdc_coeff = float(round(relevant_data_df['Round Kills'].corr(relevant_data_df['Current Equip. Value']), 3))
        return mdc_coeff if not math.isnan(mdc_coeff) else 0

    @staticmethod
    def calculate_kpr(relevant_data_df):
        total_kills = relevant_data_df['Round Kills'].sum(skipna=True)
        total_rounds = relevant_data_df.shape[0]

        if total_kills == 0 or total_rounds == 0:
            return 0
        else:
            return float(round(total_kills / total_rounds, 2))

    @staticmethod
    def calculate_kas(relevant_data_df, prev_kill_count, prev_assist_count, prev_death_count):
        kas_count = 0

        # Check rest of rounds
        for i in range(0, relevant_data_df.shape[0]):
            if relevant_data_df['Round Kills'].iloc[i] > 0 or \
               relevant_data_df['Kills'].iloc[i] > prev_kill_count or \
               relevant_data_df['Assists'].iloc[i] > prev_assist_count or \
               relevant_data_df['Deaths'].iloc[i] == prev_death_count:
                kas_count += 1

            prev_kill_count = relevant_data_df['Kills'].iloc[i]
            prev_assist_count = relevant_data_df['Assists'].iloc[i]
            prev_death_count = relevant_data_df['Deaths'].iloc[i]

        if kas_count == 0:
            return 0

        return round(kas_count / relevant_data_df.shape[0], 2) * 100

    @staticmethod
    def calculate_kdr_kda(relevant_data_df, prev_side_kills, prev_side_assists, prev_side_deaths):
        last_entry = relevant_data_df.iloc[-1]

        kill_total = last_entry['Kills'] - prev_side_kills
        assist_total = last_entry['Assists'] - prev_side_assists
        death_total = last_entry['Deaths'] - prev_side_deaths

        kdr = float(round(kill_total / death_total, 3))
        kda = float(round((kill_total + assist_total) / death_total, 3))
        return kdr, kda
