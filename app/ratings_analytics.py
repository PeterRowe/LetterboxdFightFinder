import pandas as pd
from copy import deepcopy


class RatingsAnalytics():
    """
    Class for storing methods which perform analytics based on the scraped datafram of ratings
    """
    def __init__(self, ratings_dataframe: pd.DataFrame):
        self.ratings_dataframe = ratings_dataframe

    def get_differences_in_ratings(self) -> pd.Series:
        """
        Gets the differences between the ratings of the user in the first column in self.ratings_dataframe
        and the ratings of the users in subsequent columns. These differences are packaged into a series
        and orderd by the biggest difference to smallest
        :returns: A pandas Series containing the difference in film ratings ordered by biggest to smallest difference
        """
        ratings_differences = deepcopy(self.ratings_dataframe[self.ratings_dataframe.columns[1::]])
        for user in list(ratings_differences):
            ratings_differences[user] = abs(ratings_differences[user] - self.ratings_dataframe[self.ratings_dataframe.columns[0]])

        columns = ratings_differences.columns
        index = ratings_differences.index
        values = ratings_differences.to_numpy()
        
        differences = ratings_differences.stack().sort_values(ascending=False)
