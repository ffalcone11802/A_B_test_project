import requests
import environ
env = environ.Env()
environ.Env.read_env()


class TMDBUtils:
    """
    Custom class to manage interaction with TMDB API
    """
    __request_path = "https://api.themoviedb.org/3/movie/"
    __img_path = "https://image.tmdb.org/t/p/w"
    __additional_info = {
        'backdrop_path': __img_path + '780',
        'poster_path': __img_path + '500'
    }

    def populate(self, recs):
        recommendations_data = []
        for item_id in recs:
            response = requests.get(
                self.__request_path + item_id,
                params={'api_key': env('API_KEY')}
            )
            item = response.json()
            # Adding path to images
            item = self.add_info(item)
            recommendations_data.append(item)

        return recommendations_data

    def add_info(self, item):
        for field in item.keys():
            if field in self.__additional_info.keys() and item[field]:
                item[field] = self.__additional_info[field] + item[field]
        return item
