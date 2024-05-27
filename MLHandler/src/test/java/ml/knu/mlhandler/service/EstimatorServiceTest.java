package ml.knu.mlhandler.service;

import ml.knu.mlhandler.dto.external.MLResponse;
import ml.knu.mlhandler.dto.external.MlRequest;
import ml.knu.mlhandler.dto.external.TokenizeRequest;
import ml.knu.mlhandler.dto.external.TokenizeResponse;
import ml.knu.mlhandler.dto.external.TokenizeResponseUnit;
import ml.knu.mlhandler.dto.graphql.ProcessTextsInput;
import ml.knu.mlhandler.dto.graphql.ProcessedText;
import ml.knu.mlhandler.utils.ExternalRequestHandler;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentMatchers;

import java.util.List;
import java.util.Optional;

import static org.hamcrest.Matchers.any;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class EstimatorServiceTest {

  private static final String URL_TOKENIZER = "http://tokenizer/processTexts";
  private static final String URL_ML_SERVICE = "http://mlservice/predict";
  private static final ProcessTextsInput INPUT =
      ProcessTextsInput.builder()
          .texts(List.of("Hello", "World"))
          .model("RNN")
          .isInModel(true)
          .build();
  private static final TokenizeResponse TOKENIZE_RESPONSE =
      TokenizeResponse.builder()
          .processed(List.of(
              TokenizeResponseUnit.builder().text("Hello").processed("hello").build(),
              TokenizeResponseUnit.builder().text("World").processed("world").build()))
          .build();

  private ExternalRequestHandler requestHandler;

  private EstimatorService estimatorService;

  @BeforeEach
  void setUp() {
    requestHandler = mock(ExternalRequestHandler.class);
    estimatorService = new EstimatorService(requestHandler, "http://tokenizer", "http://mlservice");
  }

  @Test
  void predictSuccessfulFlow() {
    MLResponse mlResponse = new MLResponse(
        List.of(
            ProcessedText.builder().text("Hello").predicted("Positive").build(),
            ProcessedText.builder().text("World").predicted("Positive").build()
        ));

    when(requestHandler.post(eq(URL_TOKENIZER), ArgumentMatchers.any(), eq(TokenizeResponse.class)))
        .thenReturn(Optional.of(TOKENIZE_RESPONSE));
    when(requestHandler.post(eq(URL_ML_SERVICE), ArgumentMatchers.any(), eq(MLResponse.class)))
        .thenReturn(Optional.of(mlResponse));

    List<ProcessedText> result = estimatorService.predict(INPUT);

    assertEquals(2, result.size());
    assertEquals("Positive", result.get(0).getPredicted());
  }

  @Test
  void predictFailedTokenizeResponse() {
    when(requestHandler.post(URL_TOKENIZER, new TokenizeRequest(INPUT), TokenizeResponse.class))
        .thenReturn(Optional.empty());

    List<ProcessedText> result = estimatorService.predict(INPUT);

    assertTrue(result.stream().allMatch(e -> "Error".equals(e.getPredicted())));
  }

  @Test
  void predictFailedMlResponse() {
    when(requestHandler.post(URL_TOKENIZER, new TokenizeRequest(INPUT), TokenizeResponse.class))
        .thenReturn(Optional.of(TOKENIZE_RESPONSE));
    when(requestHandler.post(URL_ML_SERVICE, any(MlRequest.class), MLResponse.class))
        .thenReturn(Optional.empty());

    List<ProcessedText> result = estimatorService.predict(INPUT);

    assertTrue(result.stream().allMatch(e -> "Error".equals(e.getPredicted())));
  }
}