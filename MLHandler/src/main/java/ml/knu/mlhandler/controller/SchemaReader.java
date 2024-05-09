package ml.knu.mlhandler.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class SchemaReader {

  @GetMapping("/")
  public String home() {
    return "apiDoc.html";
  }

  @GetMapping("/apidoc")
  public String apiDoc() {
    return "apiDoc.html";
  }
}
