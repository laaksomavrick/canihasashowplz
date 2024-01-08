from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin


class IsLikedTransformer(TransformerMixin, BaseEstimator):
    def __init__(self):
        self.columns = ["IsLiked"]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        for col in self.columns:
            X_copy[col] = (
                X_copy[col].map({"True": True, "False": False}).fillna(X_copy[col])
            )

        return X_copy


class ShowUserEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, encoder=LabelEncoder()):
        self.encoder = encoder
        super()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X["UserIdEncoded"] = self.encoder.fit_transform(X["UserId"])
        X["ShowIdEncoded"] = self.encoder.fit_transform(X["ShowId"])
        return X


class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.drop(columns=self.columns_to_drop, errors="ignore")
        return X


class DropDuplicates(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop_dupes):
        self.columns_to_drop_dupes = columns_to_drop_dupes

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.drop_duplicates(subset=self.columns_to_drop_dupes)
        return X


class PivotShowIds(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.pivot(
            index="UserIdEncoded", columns="ShowIdEncoded", values="IsLiked"
        ).fillna(0)
        return X
