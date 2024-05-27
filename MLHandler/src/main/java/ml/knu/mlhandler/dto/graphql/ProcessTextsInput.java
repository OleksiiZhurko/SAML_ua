package ml.knu.mlhandler.dto.graphql;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.util.List;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class ProcessTextsInput {

  private String model;
  private Boolean isInModel;
  private List<String> texts;
}
