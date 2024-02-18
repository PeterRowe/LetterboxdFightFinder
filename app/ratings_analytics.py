import pandas as pd
from copy import deepcopy


class RatingsAnalytics():
    """
    Class for storing methods which perform analytics based on the scraped datafram of ratings
    """
    def get_differences_in_ratings(self, ratings_dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Gets the differences between the ratings of the user in the first column in self.ratings_dataframe
        and the ratings of the users in subsequent columns. These differences are packaged into a series
        and orderd by the biggest difference to smallest
        :returns: A pandas Dataframe with columns "Film", "Rating difference", "Mutual", "mMutual Rating", "User Rating"
        """
        all_mutuals_differences = pd.DataFrame()
        all_mutuals_ratings = deepcopy(ratings_dataframe[ratings_dataframe.columns[1::]])
        for mutual in list(all_mutuals_ratings):
            mutual_differences = abs(all_mutuals_ratings[mutual] - ratings_dataframe[ratings_dataframe.columns[0]])
            mutual_differences = mutual_differences.reset_index(name="Rating difference") # Changing film titles from index to columns
            mutual_differences = mutual_differences.rename(columns={"index": "Film"})
            mutual_differences["Mutual"] = mutual
            mutual_differences["Mutual Rating"] = all_mutuals_ratings[mutual].array
            mutual_differences["User Rating"] = ratings_dataframe[ratings_dataframe.columns[0]].array
            all_mutuals_differences = pd.concat([all_mutuals_differences, mutual_differences])

        all_mutuals_differences = all_mutuals_differences.sort_values(by=["Rating difference", "Mutual"], ascending=[False, True])
        return all_mutuals_differences