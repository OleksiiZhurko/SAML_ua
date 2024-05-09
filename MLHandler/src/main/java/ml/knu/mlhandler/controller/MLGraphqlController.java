package ml.knu.mlhandler.controller;

import ml.knu.mlhandler.dto.graphql.MLModel;
import ml.knu.mlhandler.dto.graphql.ProcessTextsInput;
import ml.knu.mlhandler.dto.graphql.ProcessedText;
import ml.knu.mlhandler.service.EstimatorService;
import ml.knu.mlhandler.service.ModelsService;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.ArrayList;
import java.util.List;

@Controller
public class MLGraphqlController {

  private final ModelsService modelsService;
  private final EstimatorService estimatorService;

  public MLGraphqlController(ModelsService modelsService, EstimatorService estimatorService) {
    this.modelsService = modelsService;
    this.estimatorService = estimatorService;
  }

  @QueryMapping
  public List<MLModel> models() {
    return modelsService.getModels();
  }

  @QueryMapping
  public List<ProcessedText> processTexts(@Argument("input") ProcessTextsInput input) {
    return estimatorService.predict(input);
  }
}
