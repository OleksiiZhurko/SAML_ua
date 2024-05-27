package ml.knu.mlhandler.controller;

import ml.knu.mlhandler.dto.graphql.MLModel;
import ml.knu.mlhandler.dto.graphql.ProcessTextsInput;
import ml.knu.mlhandler.dto.graphql.ProcessedText;
import ml.knu.mlhandler.service.EstimatorService;
import ml.knu.mlhandler.service.ModelsService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class MLGraphqlControllerTest {

  @Mock
  private ModelsService modelsService;

  @Mock
  private EstimatorService estimatorService;

  @InjectMocks
  private MLGraphqlController controller;

  @Test
  void modelsWhenCalledShouldReturnListOfModels() {
    List<MLModel> expectedModels = List.of(
        new MLModel("SVM", "Type1"),
        new MLModel("RNN", "Type2")
    );
    when(modelsService.getModels()).thenReturn(expectedModels);

    List<MLModel> result = controller.models();

    assertNotNull(result);
    assertEquals(expectedModels, result);
  }

  @Test
  void processTextsWhenCalledWithInputShouldReturnListOfProcessedTexts() {
    ProcessTextsInput input = ProcessTextsInput.builder().texts(List.of("Text1", "Text2")).build();
    List<ProcessedText> expectedProcessedTexts = Arrays.asList(
        ProcessedText.builder().text("Text1").predicted("Predicted1").build(),
        ProcessedText.builder().text("Text2").predicted("Predicted2").build()
    );
    when(estimatorService.predict(input)).thenReturn(expectedProcessedTexts);

    List<ProcessedText> result = controller.processTexts(input);

    assertNotNull(result);
    assertEquals(expectedProcessedTexts, result);
  }
}