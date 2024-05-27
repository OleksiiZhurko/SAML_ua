package ml.knu.mlhandler.controller;

import jakarta.servlet.http.HttpServletRequest;
import ml.knu.mlhandler.dto.external.Error;
import ml.knu.mlhandler.dto.internal.RequestDetails;
import ml.knu.mlhandler.service.RequestHandler;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CustomErrorControllerTest {

  @Mock
  private HttpServletRequest request;

  @Mock
  private RequestHandler requestHandler;

  @InjectMocks
  private CustomErrorController errorController;

  @Test
  void handleErrorWhenStatusIsNotNullShouldReturnErrorDetails() {
    RequestDetails details = new RequestDetails(HttpStatus.NOT_FOUND, "/not-found");
    when(requestHandler.extractError(request)).thenReturn(details);

    ResponseEntity<Error> response = errorController.handleError(request);

    assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    assertEquals(HttpStatus.NOT_FOUND.value(), response.getBody().getStatus());
    assertEquals(HttpStatus.NOT_FOUND.getReasonPhrase(), response.getBody().getReason());
    assertEquals("/not-found", response.getBody().getPath());
  }

  @Test
  void handleErrorWhenStatusIsNullShouldReturnInternalServerError() {
    RequestDetails details = new RequestDetails(null, "/unknown-error");
    when(requestHandler.extractError(request)).thenReturn(details);

    ResponseEntity<Error> response = errorController.handleError(request);

    assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
    assertEquals(HttpStatus.INTERNAL_SERVER_ERROR.value(), response.getBody().getStatus());
    assertEquals(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase(), response.getBody().getReason());
    assertEquals("/unknown-error", response.getBody().getPath());
  }
}