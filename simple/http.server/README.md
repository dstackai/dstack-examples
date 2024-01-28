# A simple service (HTTP server)

This is one of the simplest examples that demonstrates how to use services.

This service runs Python's `http.server`.

To deploy this service, execute the following command from the root directory of the repo:

```shell
dstack run . -f simple/http.server/serve.dstack.yml
```

For more details on how services work, refer to [dstack.ai/docs/concepts/services](https://dstack.ai/docs/concepts/services).