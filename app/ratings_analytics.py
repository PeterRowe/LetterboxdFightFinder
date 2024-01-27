import pandas as pd
from copy import deepcopy


class RatingsAnalytics():
    """
    Class for storing methods which perform analytics based on the scraped datafram of ratings
    """
    def get_differences_in_ratings(self, ratings_dataframe: pd.DataFrame) -> list[tuple[tuple, float]]:
        """
        Gets the differences between the ratings of the user in the first column in self.ratings_dataframe
        and the ratings of the users in subsequent columns. These differences are packaged into a series
        and orderd by the biggest difference to smallest
        :returns: A list of tuples containing a tuple of film name and user and a float storing the difference.
                  In the format ((<film_name>, <user>), <difference_in_rating>)
        """
        ratings_differences = deepcopy(ratings_dataframe[ratings_dataframe.columns[1::]])
        for user in list(ratings_differences):
            ratings_differences[user] = abs(ratings_differences[user] - ratings_dataframe[ratings_dataframe.columns[0]])

        columns = ratings_differences.columns
        index = ratings_differences.index
        values = ratings_differences.to_numpy()
        
        differences = ratings_differences.stack().sort_values(ascending=False)
        return list(differences.items())
