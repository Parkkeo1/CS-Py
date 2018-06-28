import pandas as pd
import math


class MatchDataSummary:

    def __init__(self, round_data_df):
        self.data_frame = round_data_df

        # simple properties
        self.duration = self.data_frame['Time'].iloc[-1] - self.data_frame['Time'].iloc[0] # TODO: Fix to minutes, not seconds
        self.round_count = self.data_frame.shape[0]
        self.map_name = self.data_frame['Map'].iloc[-1]

        # to-be calculated properties
        self.rating1, self.ct_rating1, self.t_rating1 = 0, 0, 0
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
        ct_data = self.data_frame[self.data_frame['Player Team'] == 'CT']
        t_data = self.data_frame[self.data_frame['Player Team'] == 'T']

        # TODO: HLTV Rating 1.0
        # TODO: Kills, Assists, Survived Consistency Percentage

        # HSR: Headshot Ratio
        # MDC: Monetary Dependency Coefficient
        # KPR: Kills Per Round
        # KDR, KDA: Kill Death Ratio, Kill+Assist Death Ratio
        # MEAN: Mean Equipment Value

        # Totals
        self.hsr = self.calculate_hsr(self.data_frame)
        self.mdc = self.calculate_mdc(self.data_frame)
        self.kpr = self.calculate_kpr(self.data_frame)
        self.kdr, self.kda = self.calculate_kdr_kda(self.data_frame)
        self.mean_equip = int(round(self.data_frame['Current Equip. Value'].mean(skipna=True)))

        # CT
        if not ct_data.empty:
            self.ct_hsr = self.calculate_hsr(ct_data)
            self.ct_mdc = self.calculate_mdc(ct_data)
            self.ct_kpr = self.calculate_kpr(ct_data)
            self.ct_kdr, self.ct_kda = self.calculate_kdr_kda(ct_data)
            self.ct_mean_equip = int(round(ct_data['Current Equip. Value'].mean(skipna=True)))

        # T
        if not t_data.empty:
            self.t_hsr = self.calculate_hsr(t_data)
            self.t_mdc = self.calculate_mdc(t_data)
            self.t_kpr = self.calculate_kpr(t_data)
            self.t_kdr, self.t_kda = self.calculate_kdr_kda(t_data)
            self.t_mean_equip = int(round(t_data['Current Equip. Value'].mean(skipna=True)))

    @staticmethod
    def calculate_rating(relevant_data_df):
        pass

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
    def calculate_kas(relevant_data_df):
        pass

    @staticmethod
    def calculate_kdr_kda(relevant_data_df):
        last_entry = relevant_data_df.iloc[-1]
        kdr = float(round(last_entry['Kills'] / last_entry['Deaths'], 3))
        kda = float(round((last_entry['Kills'] + last_entry['Assists']) / last_entry['Deaths'], 3))
        return kdr, kda


