package ml.knu.mlhandler.service;

import ml.knu.mlhandler.dto.external.MLModelsResponse;
import ml.knu.mlhandler.dto.graphql.MLModel;
import ml.knu.mlhandler.utils.ExternalRequestHandler;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class ModelsServiceTest {

  private static final String URL_MODELS = "https://test.com/api/models";

  private ExternalRequestHandler requestHandler;

  private ModelsService modelsService;

  @BeforeEach
  void setUp() {
    requestHandler = mock(ExternalRequestHandler.class);
    modelsService = new ModelsService(requestHandler, "https://test.com/api");
  }

  @Test
  void getModelsWhenServiceReturnsModelsShouldReturnListOfModels() {
    MLModelsResponse response =
        MLModelsResponse.builder()
            .models(
                List.of(
                    new MLModel("SVM", "Description1"),
                    new MLModel("RNN", "Description2")
                ))
            .build();
    when(requestHandler.get(URL_MODELS, MLModelsResponse.class)).thenReturn(Optional.of(response));

    List<MLModel> models = modelsService.getModels();

    assertEquals(2, models.size());
    assertEquals("SVM", models.get(0).getName());
    assertEquals("Description1", models.get(0).getDescription());
  }

  @Test
  void getModelsWhenServiceReturnsNullShouldReturnEmptyList() {
    when(requestHandler.get(URL_MODELS, MLModelsResponse.class)).thenReturn(Optional.empty());

    List<MLModel> models = modelsService.getModels();

    assertEquals(Collections.emptyList(), models);
  }
}