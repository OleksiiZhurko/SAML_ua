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
public class TokenizeResponseUnit {

  private Boolean isInModel;
  private String missingLemmas;
  private String processed;
  private String text;
}
