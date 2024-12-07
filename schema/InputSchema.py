from pydantic import BaseModel

class InputSchema:
    def __init__(self):
        # self.user_id = None
        self.user_query = ''
        self.number_of_recommendations = None
        self.category = None
        self.rating_packaging = None
        self.rating_price = None
        self.rating_quality = None
        self.rating_service = None
        self.rating_shipping = None
        self.rating_taste = None
        # self.avg_rating = None
        self.sentiment_score = 1


    def get_all_input_with_query(self):
        ratings = {
            "rating_packaging": self.rating_packaging,
            "rating_price": self.rating_price,
            "rating_quality": self.rating_quality,
            "rating_service": self.rating_service,
            "rating_shipping": self.rating_shipping,
            "rating_taste": self.rating_taste,
        }

        # Validate that all ratings are >= 1
        for rating_name, rating_value in ratings.items():
            if rating_value < 1:
                raise ValueError(f"{rating_name} must be greater than or equal to 1")

        return {
            "user_query": self.user_query,
            **ratings,
            "sentiment_score": self.sentiment_score
        }


    def get_all_input(self):
        return {
            # "user_id": self.user_id,
            "rating_packaging": self.rating_packaging,
            "rating_price": self.rating_price,
            "rating_quality": self.rating_quality,
            "rating_service": self.rating_service,
            "rating_shipping": self.rating_shipping,
            "rating_taste": self.rating_taste,
            # "avg_rating": self.avg_rating,
            "sentiment_score": self.sentiment_score
        }

    # def get_user_id(self):
    #     return self.user_id


    def get_user_query(self):
        return self.user_query


    def get_category(self):
        return self.category

    def get_rating_columns_list(self):
        return [
            "rating_packaging",
            "rating_price",
            "rating_quality",
            "rating_service",
            "rating_shipping",
            "rating_taste",
            # "avg_rating",
            "sentiment_score"
        ]

    def get_rating_maps(self):
        return {
            "rating_packaging": self.rating_packaging,
            "rating_price": self.rating_price,
            "rating_quality": self.rating_quality,
            "rating_service": self.rating_service,
            "rating_shipping": self.rating_shipping,
            "rating_taste": self.rating_taste,
            # "avg_rating": self.avg_rating,
            "sentiment_score": self.sentiment_score
        }
    
    def get_number_of_recommendations(self):
        return self.number_of_recommendations
    
    def handle_data(self, data):
        # self.user_id = data['UserId']
        self.number_of_recommendations = data['NumberOfReccomendations']
        self.user_query = data['UserQuery']
        self.category = data['Category']
        self.rating_packaging = data['RatingPackaging']
        self.rating_price = data['RatingPrice']
        self.rating_quality = data['RatingQuality']
        self.rating_service = data['RatingService']
        self.rating_shipping = data['RatingShipping']
        self.rating_taste = data['RatingTaste']
        # self.avg_rating = data['AvgRating']

    # def set_user_id(self, user_id):
    #     self.user_id = user_id
    
    def set_rating_maps(self, rating_packaging, rating_price, rating_quality, rating_service, rating_shipping, rating_taste, sentiment_score=1):
        self.rating_packaging = rating_packaging
        self.rating_price = rating_price
        self.rating_quality = rating_quality
        self.rating_service = rating_service
        self.rating_shipping = rating_shipping
        self.rating_taste = rating_taste
        # self.avg_rating = avg_rating
        self.sentiment_score = sentiment_score  # Always default to 1

    def set_category(self, category):
        self.category = category

    def decide_weight_map(self):
        weight_map = {
            5: 1.0,  # 5 stars
            4: 0.8,  # 4 stars
            3: 0.6,  # 3 stars
            2: 0.4,  # 2 stars
            1: 0.3   # 1 star
        }
        return weight_map

    def apply_weights_and_set_ratings(self):
        weight_map = self.decide_weight_map()
        current_weighted_ratings = self.get_rating_maps()
        for key, value in current_weighted_ratings.items():
            current_weighted_ratings[key] = weight_map[value]

        self.set_rating_maps(**current_weighted_ratings)


class InputSchemaBase(BaseModel):
    NumberOfReccomendations: int
    # UserId: int
    UserQuery: str
    Category: str
    RatingPackaging: float
    RatingPrice: float
    RatingQuality: float
    RatingService: float
    RatingShipping: float
    RatingTaste: float
    # AvgRating: float