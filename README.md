# ChromaDB Deployment for Render.com

This repository contains configuration files needed to deploy [ChromaDB](https://www.trychroma.com/) on [Render](https://render.com/). ChromaDB is an open-source embedding database built to make it easy to build LLM applications.

## Deployment Instructions

### 1. Fork or Clone the ChromaDB Repository

```bash
git clone https://github.com/chroma-core/chroma.git
cd chroma
```

### 2. Add the render.yaml File

Add the `render.yaml` file (already included in this repository) to the root of your ChromaDB repository.

### 3. Deploy to Render

1. Create a [Render account](https://dashboard.render.com/register) if you don't have one.
2. Go to the Render Dashboard.
3. Click on "New" and select "Blueprint".
4. Connect your GitHub/GitLab account and select your ChromaDB repository.
5. Render will detect the `render.yaml` file and set up the service accordingly.
6. Click "Apply" to deploy.

## Configuration Options

The `render.yaml` file includes several configuration options that you can modify based on your needs:

### Service Plan

```yaml
runtime: docker  # Use 'runtime' instead of 'env' as per current Render specs
plan: standard   # Options: starter, standard, pro, professional, business
```

Choose a plan based on your expected workload:
- starter: 512 MB RAM, 0.5 CPU
- standard: 1 GB RAM, 1 CPU
- pro: 2 GB RAM, 1 CPU
- professional: 4 GB RAM, 2 CPU
- business: 8 GB RAM, 4 CPU

### Disk Storage

```yaml
disk:
  name: chroma-data
  mountPath: /data
  sizeGB: 10  # Adjust based on your needs
```

Increase `sizeGB` if you expect to store a large number of embeddings.

### Port Configuration

```yaml
port: 8000
```

Expose the port for your ChromaDB service. The default port for ChromaDB is 8000.

### Workers

```yaml
- key: CHROMA_WORKERS
  value: 1
```

Increase the number of workers for higher throughput if your plan has more CPU cores.

### Authentication and Authorization

Uncomment and configure these sections in the `render.yaml` file if you need authentication:

```yaml
# - key: CHROMA_SERVER_AUTHN_PROVIDER
#   value: chromadb.auth.basic_authn.BasicAuthenticator
# 
# - key: CHROMA_SERVER_AUTHN_CREDENTIALS_FILE
#   value: /path/to/credentials
```

## Connecting to Your Deployed ChromaDB

Once deployed, Render will provide a URL for your service. You can connect to it from your applications:

```python
import chromadb
# Connect to your Render-hosted ChromaDB instance
client = chromadb.HttpClient(host="https://your-app-name.onrender.com")

# Create a collection
collection = client.create_collection("my_collection")

# Add documents
collection.add(
    documents=["This is a document", "This is another document"],
    metadatas=[{"source": "my_source"}, {"source": "my_source"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)
```

## Production Considerations

For production deployments, consider:

1. **Authentication**: Enable authentication using ChromaDB's auth providers.
2. **HTTPS**: Render provides HTTPS by default for all services.
3. **Backups**: Set up regular backups of your `/data` directory.
4. **Monitoring**: Use Render's built-in monitoring and logs to track your service.
5. **Scaling**: If you need more performance, upgrade to a higher-tier plan or consider Render's [Dedicated Plan](https://render.com/pricing).

## Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Render Documentation](https://render.com/docs)
- [ChromaDB GitHub Repository](https://github.com/chroma-core/chroma)
