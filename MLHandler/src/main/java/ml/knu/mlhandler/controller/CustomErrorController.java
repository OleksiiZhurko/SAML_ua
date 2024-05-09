package ml.knu.mlhandler.controller;

import jakarta.servlet.http.HttpServletRequest;
import ml.knu.mlhandler.dto.external.Error;
import ml.knu.mlhandler.dto.internal.RequestDetails;
import ml.knu.mlhandler.service.RequestHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CustomErrorController implements ErrorController {

  private final RequestHandler requestHandler;

  @Autowired
  public CustomErrorController(RequestHandler requestHandler) {
    this.requestHandler = requestHandler;
  }

  @RequestMapping("${server.error.path:/error}")
  public ResponseEntity<Error> handleError(HttpServletRequest request) {
    RequestDetails details = requestHandler.extractError(request);

    if (details.getStatus() != null) {
      return new ResponseEntity<>(
          Error.builder()
              .timestamp(System.currentTimeMillis())
              .status(details.getStatus().value())
              .reason(details.getStatus().getReasonPhrase())
              .path(details.getUri())
              .build(),
          details.getStatus()
      );
    }

    return new ResponseEntity<>(
        Error.builder()
            .timestamp(System.currentTimeMillis())
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .reason(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
            .path(details.getUri())
            .build(),
        HttpStatus.INTERNAL_SERVER_ERROR
    );
  }
}
