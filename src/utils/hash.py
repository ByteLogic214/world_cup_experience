import hashlib

def hash_string(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def hash_dataframe(df) -> str:
    return hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()
