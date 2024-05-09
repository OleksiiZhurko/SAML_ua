package ml.knu.mlhandler.dto.external;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import ml.knu.mlhandler.dto.graphql.ProcessTextsInput;

import java.util.List;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TokenizeRequest {

  private boolean isInModel;
  private List<String> texts;

  public TokenizeRequest(ProcessTextsInput input) {
    isInModel = input.getIsInModel();
    texts = input.getTexts();
  }
}
