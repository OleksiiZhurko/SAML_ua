package ml.knu.mlhandler.dto.external;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import ml.knu.mlhandler.dto.graphql.MLModel;
import ml.knu.mlhandler.dto.graphql.ProcessedText;

import java.util.List;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MLModelsResponse {

  private List<MLModel> models;
}
