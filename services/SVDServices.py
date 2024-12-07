from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

class SVDServices:
    def __init__(self, model_path='paraphrase-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
        self.df = None
        self.hybrid_similarity = None
        self.embeddings = None

    def load_data(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error loading data: {e}")

    def preprocess_df(self):
        try:
            df_copy = self.df.copy()
            df_copy['review_content'] = df_copy['review_content'].fillna('')
            df_copy['review_embedding'] = df_copy['review_content'].apply(lambda x: self.model.encode(x))

            ratings_matrix = df_copy.pivot_table(index='review_id', columns='brand_id', values='avg_rating').fillna(0)
            svd = TruncatedSVD(n_components=5)
            latent_matrix = svd.fit_transform(ratings_matrix)
            
            embeddings = np.vstack(df_copy['review_embedding'].to_numpy())
            embedding_similarity = cosine_similarity(embeddings)
            self.hybrid_similarity = 0.5 * cosine_similarity(latent_matrix) + 0.5 * embedding_similarity
            self.embeddings = embeddings
            self.df = df_copy
        except Exception as e:
            print(f"Error preprocessing data: {e}")

    def handle_user_input(self, input_object):
        user_input_embedding = self.model.encode(input_object['user_query'])
        user_input_embedding = user_input_embedding.reshape(1, -1)
        return user_input_embedding

    def calculate_combined_similarity(self, user_input_embedding):
        embedding_similarity = cosine_similarity(user_input_embedding, self.embeddings).flatten()
        latent_matrix_similarity = self.hybrid_similarity.mean(axis=0)
        combined_similarity = 0.5 * latent_matrix_similarity + 0.5 * embedding_similarity
        return combined_similarity

    def svd_recommendation(self, input_object, num_recommendations=30):
        try:
            user_input_embedding = self.handle_user_input(input_object)
            similarity_scores = self.calculate_combined_similarity(user_input_embedding)
            similar_reviews = list(enumerate(similarity_scores))
            similar_reviews = sorted(similar_reviews, key=lambda x: x[1], reverse=True)
            recommended_brands = set()
            selected_rows = []

            for i in similar_reviews:
                brand_id = self.df.iloc[i[0]]['brand_id']
                if brand_id not in recommended_brands:
                    recommended_brands.add(brand_id)
                    selected_rows.append(i[0])
                if len(recommended_brands) == num_recommendations:
                    break

            filtered_df = self.df.iloc[selected_rows]
            return filtered_df
        except Exception as e:
            print(f"Error in svd_recommendation: {e}")
            return pd.DataFrame()