>  docker build -t demand_forecasr_api:latest . - To create an image

>  docker run --rm -it --entrypoint /bin/bash demand_forecasting_api:latest - To start the container and see its contents

>  docker run -d --name demand_forecast-api -p 8000:8000 demand_forecast_api:latest - 
      After creating image , crate a continer with name   demand_forecast_api from image name demand_forecast_api:latest

> docker rm grafana-credentials-fix grafana-old alertmanager  ( to remove stopped containers)

> docker tag oldname:latest newname

> docker run --rm --entrypoint python demand_forecasr_api:latest -c "import pythonjsonlogger; print('python-json-logger OK')"

> Moutning AWS credintial to docker
> dir "%USERPROFILE%\.aws"
> docker run -d --name api_container -p 8000:8000 -v "%USERPROFILE%\.aws:/root/.aws:ro" api_image:latest

> docker cp grafana:/var/lib/grafana ./grafana_backup
> docker run --rm \
  -v grafana_data:/target \
  -v "D:\...\grafana_backup:/source:ro" \
  alpine \
  sh -c "cp -a /source/. /target/"

> docker run --rm -v grafana_data:/data alpine ls -la /data