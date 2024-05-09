package ml.knu.mlhandler.service;

import ml.knu.mlhandler.dto.external.MLModelsResponse;
import ml.knu.mlhandler.dto.external.MLRequestUnit;
import ml.knu.mlhandler.dto.external.MLResponse;
import ml.knu.mlhandler.dto.external.MlRequest;
import ml.knu.mlhandler.dto.external.TokenizeRequest;
import ml.knu.mlhandler.dto.external.TokenizeResponse;
import ml.knu.mlhandler.dto.graphql.MLModel;
import ml.knu.mlhandler.dto.graphql.ProcessTextsInput;
import ml.knu.mlhandler.dto.graphql.ProcessedText;
import ml.knu.mlhandler.utils.ExternalRequestHandler;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

@Service
public class ModelsService {

  private final ExternalRequestHandler requestHandler;

  private final String msServiceUrl;

  public ModelsService(
      ExternalRequestHandler requestHandler,
      @Value("${internal.url.mlservice}") String msServiceUrl
  ) {
    this.requestHandler = requestHandler;
    this.msServiceUrl = msServiceUrl + "/models";
  }

  public List<MLModel> getModels() {
    return requestHandler.get(msServiceUrl, MLModelsResponse.class)
        .map(MLModelsResponse::getModels)
        .orElse(Collections.emptyList());
  }
}
