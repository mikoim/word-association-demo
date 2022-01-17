import { Configuration, DefaultApi } from "@/client";

export function clientFactory(): DefaultApi {
  let url = "http://0.0.0.0:8888";

  if (process.env.NODE_ENV === "production") {
    url = window.location.origin;
  }

  return new DefaultApi(new Configuration({ basePath: url }));
}
