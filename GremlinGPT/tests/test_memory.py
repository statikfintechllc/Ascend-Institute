from memory.vector_store.embedder import embed_text, package_embedding


def test_embedding_store():
    text = "GremlinGPT stores vector embeddings locally."
    vec = embed_text(text)
    assert len(vec) > 0

    embed = package_embedding(text, vec, {"test_case": True})
    assert "embedding" in embed and "meta" in embed
