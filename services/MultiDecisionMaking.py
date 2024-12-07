import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class MultiDecisionMaking:
    def __init__(self, top_brands_df, category, weights_map, top_n=5):
        self.scaler = MinMaxScaler()
        self.top_brands_df = top_brands_df
        self.category = category
        self.rating_columns = ["rating_packaging", "rating_price", "rating_quality", "rating_service", "rating_shipping", "rating_taste", "sentiment_score"]
        self.weights_map = weights_map
        self.top_n = top_n

    def make_decision(self):
        try:
            df_norm = self.normalize_top_brands_df()
            weighted_df, rating_priorities, weights = self.assign_weights(df_norm, self.weights_map)
            ideal_score, worst_score = self.find_ideal_worst_score(weighted_df, rating_priorities)
            distance_to_ideal_solution, distance_to_worst_solution = self.calculate_euclidean_distance(weighted_df, ideal_score, worst_score, rating_priorities)
            df_with_similarity_score = self.calculate_similarity_score(weighted_df, distance_to_ideal_solution, distance_to_worst_solution)
            top_n_brands_df = self.get_top_n_brands_df(df_with_similarity_score, self.top_n)
            top_n_brands_list = self.get_top_n_brands_list(top_n_brands_df)
            return top_n_brands_list
        except Exception as e:
            print(f"Error in make_decision: {e}")
            return []

    def normalize_top_brands_df(self):
        try:
            df_norm = self.top_brands_df.copy()
            df_norm = df_norm[df_norm['display_name'] == self.category]
            df_norm[self.rating_columns] = self.scaler.fit_transform(df_norm[self.rating_columns])
            return df_norm
        except Exception as e:
            print(f"Error in normalize_top_brands_df: {e}")
            return pd.DataFrame()

    def assign_weights(self, df_norm, weights_map):
        try:
            rating_priorities = list(weights_map.keys())
            weights = list(weights_map.values())
            weighted_df = df_norm.copy()
            weighted_df[rating_priorities] = weighted_df[rating_priorities].multiply(weights, axis=1)
            return weighted_df, rating_priorities, weights
        except Exception as e:
            print(f"Error in assign_weights: {e}")
            return pd.DataFrame(), [], []

    def find_ideal_worst_score(self, weighted_df, rating_priorities):
        try:
            ideal_score = weighted_df[rating_priorities].max(axis=0)
            worst_score = weighted_df[rating_priorities].min(axis=0)
            return ideal_score, worst_score
        except Exception as e:
            print(f"Error in find_ideal_worst_score: {e}")
            return pd.Series(), pd.Series()

    def calculate_euclidean_distance(self, weighted_df, ideal_score, worst_score, rating_priorities):
        try:
            weighted_rating_matrix = weighted_df[rating_priorities]
            distance_to_ideal_solution = np.sqrt((weighted_rating_matrix - ideal_score)**2).sum(axis=1)
            distance_to_worst_solution = np.sqrt((weighted_rating_matrix - worst_score)**2).sum(axis=1)
            return distance_to_ideal_solution, distance_to_worst_solution
        except Exception as e:
            print(f"Error in calculate_euclidean_distance: {e}")
            return np.array([]), np.array([])

    def calculate_similarity_score(self, weighted_df, distance_to_ideal_solution, distance_to_worst_solution):
        try:
            similarity_score = distance_to_worst_solution / (distance_to_ideal_solution + distance_to_worst_solution)
            df_with_similarity_score = weighted_df.copy()
            df_with_similarity_score['similarity_score'] = similarity_score
            return df_with_similarity_score
        except Exception as e:
            print(f"Error in calculate_similarity_score: {e}")
            return pd.DataFrame()

    def get_top_n_brands_df(self, df_with_similarity_score, top_n):
        try:
            top_n_brands_df = df_with_similarity_score.nlargest(top_n, 'similarity_score')
            return top_n_brands_df
        except Exception as e:
            print(f"Error in get_top_n_brands_df: {e}")
            return pd.DataFrame()

    def get_top_n_brands_list(self, top_n_brands_df):
        try:
            top_n_brands_list = top_n_brands_df['brand_id'].tolist()
            return top_n_brands_list
        except Exception as e:
            print(f"Error in get_top_n_brands_list: {e}")
            return []