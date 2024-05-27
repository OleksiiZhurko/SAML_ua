package ml.knu.mlhandler.service;

import ml.knu.mlhandler.dto.external.MLRequestUnit;
import ml.knu.mlhandler.dto.external.MLResponse;
import ml.knu.mlhandler.dto.external.MlRequest;
import ml.knu.mlhandler.dto.external.TokenizeRequest;
import ml.knu.mlhandler.dto.external.TokenizeResponse;
import ml.knu.mlhandler.dto.graphql.Probabilities;
import ml.knu.mlhandler.dto.graphql.ProcessTextsInput;
import ml.knu.mlhandler.dto.graphql.ProcessedText;
import ml.knu.mlhandler.utils.ExternalRequestHandler;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

@Service
public class EstimatorService {

  private final ExternalRequestHandler requestHandler;
  private final String tokenizerUrl;

  private final String msServiceUrl;

  public EstimatorService(
      ExternalRequestHandler requestHandler,
      @Value("${internal.url.tokenizer}") String tokenizerUrl,
      @Value("${internal.url.mlservice}") String msServiceUrl
  ) {
    this.requestHandler = requestHandler;
    this.tokenizerUrl = tokenizerUrl + "/processTexts";
    this.msServiceUrl = msServiceUrl + "/predict";
  }

  public List<ProcessedText> predict(ProcessTextsInput input) {
    return requestHandler.post(tokenizerUrl, new TokenizeRequest(input), TokenizeResponse.class)
        .map(TokenizeResponse::getProcessed)
        .map(units ->
            MlRequest.builder()
                .model(input.getModel())
                .toPredict(units.stream()
                    .map(unit -> MLRequestUnit.builder()
                        .text(unit.getText())
                        .lemmas(unit.getProcessed())
                        .build())
                    .toList())
                .build())
        .map(request -> requestHandler.post(msServiceUrl, request, MLResponse.class))
        .map(response -> response.map(MLResponse::getPredicted)
            .orElse(prepareUnprocessed(input)))
        .orElse(prepareUnprocessed(input));
  }

  private List<ProcessedText> prepareUnprocessed(ProcessTextsInput input) {
    return input.getTexts().stream()
        .map(text ->
            ProcessedText.builder()
                .model(input.getModel())
                .predicted("Error")
                .probabilities(new Probabilities())
                .text(text)
                .build())
        .toList();
  }
}
