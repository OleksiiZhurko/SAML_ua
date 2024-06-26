package ml.knu.mlhandler.dto.graphql;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProcessedText {

  private String model;
  private String text;
  private String predicted;
  private Probabilities probabilities;
}
