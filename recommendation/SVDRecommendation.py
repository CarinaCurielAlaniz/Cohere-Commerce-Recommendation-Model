from services.MultiDecisionMaking import MultiDecisionMaking
from services.SVDServices import SVDServices

class SVDRecommendation:
    _svd_services = None

    def __init__(self, category, weights_map, top_n=5, data_path="data/cleaned_df.csv", model_path='paraphrase-MiniLM-L6-v2'):
        self.category = category
        self.weights_map = weights_map
        self.top_n = top_n
        self.data_path = data_path
        self.model_path = model_path

        if SVDRecommendation._svd_services is None:
            SVDRecommendation._svd_services = SVDServices(model_path)
            try:
                SVDRecommendation._svd_services.load_data(data_path)
                SVDRecommendation._svd_services.preprocess_df()
            except Exception as e:
                print(f"Error initializing SVDRecommendation: {e}")

    def svd_recommendation(self, input_object, num_recommendations=40, top_n=5):
        try:
            top_brands_df = SVDRecommendation._svd_services.svd_recommendation(input_object, num_recommendations)
            multi_decision_making = MultiDecisionMaking(top_brands_df, self.category, self.weights_map, top_n)
            top_n_brands_list = multi_decision_making.make_decision()
            return top_n_brands_list
        except Exception as e:
            print(f"Error in svd_recommendation: {e}")
            return []