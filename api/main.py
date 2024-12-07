from fastapi import FastAPI
from recommendation.SVDRecommendation import SVDRecommendation
from schema.InputSchema import InputSchema, InputSchemaBase
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow the frontend to access the backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# This is just a hardcoded input schema for testing purposes
def set_input_schema():
    try:
        input_schema = InputSchema()
        # input_schema.set_user_id(0)
        input_schema.set_category('Snacks')
        input_schema.set_rating_maps(0.70682274, 0.60170271, 0.77066022, 0.96349508,  0.96349508, 0.27436838, 0.74358268, 1)
        return input_schema
    except Exception as e:
        print(f"Error in set_input_schema: {e}")
        return None

@app.get("/")
def home():
    return "Hello world"


# This is just a test get endpoint to check if the recommendation is working
@app.get("/recommend")
def recommend():
    try:
        input_schema = set_input_schema()
        if input_schema is None:
            return {"error": "Failed to set input schema"}
        category = input_schema.get_category()
        weights_map = input_schema.get_rating_maps()
        svd_recommendation = SVDRecommendation(category, weights_map)

        # The 0 parameter is the user id, we would love to change this
        top_n_brands_list = svd_recommendation.svd_recommendation(0, 40, 5)
        return top_n_brands_list
    except Exception as e:
        print(f"Error in recommend endpoint: {e}")
        return {"error": "Failed to get recommendations"}


# post endpoint to get recommendations using Input schema
# This work but this is not the kind of Input we really want to see because of the user id
@app.post("/svdrecommend")
async def svd_recommend(input_schema: InputSchemaBase):
    try:
        input_handler = InputSchema()
        data = input_schema.dict()

        # Validate input data
        if not data:
            return {"error": "Input data cannot be empty"}

        input_handler.handle_data(data)

        # Validate required fields
        category = input_handler.get_category()
        if not category:
            return {"error": "Category is required"}

        number_of_recommendations = input_handler.get_number_of_recommendations()
        if not isinstance(number_of_recommendations, int) or number_of_recommendations <= 0:
            return {"error": "Number of recommendations must be a positive integer"}

        try:
            input_object = input_handler.get_all_input_with_query()
        except ValueError as e:
            return {"error": str(e)}

        if not input_object:
            return {"error": "Input object cannot be empty"}

        input_handler.apply_weights_and_set_ratings()
        print(input_handler.get_rating_maps())

        svd_recommendation = SVDRecommendation(category, input_handler.get_rating_maps())
        top_n_brands_list = svd_recommendation.svd_recommendation(input_object, 20, number_of_recommendations)
        return top_n_brands_list

    except KeyError as e:
        return {"error": f"Missing key in input data: {e}"}
    except Exception as e:
        return {"error": f"Failed to get recommendations: {e}"}
'''
TODO: Handle case where the user id is not provided in the input data.
TODO: Handle case where the user id is in input data.
'''
