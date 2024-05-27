package ml.knu.mlhandler.service;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.http.HttpServletRequest;
import ml.knu.mlhandler.dto.internal.RequestDetails;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RequestHandlerTest {

  @Mock
  private HttpServletRequest request;

  @InjectMocks
  private RequestHandler requestHandler;

  @Test
  void extractErrorWithStatusCodeAndUri() {
    when(request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE)).thenReturn(404);
    when(request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI)).thenReturn("/not-found");

    RequestDetails details = requestHandler.extractError(request);

    assertEquals(HttpStatus.NOT_FOUND, details.getStatus());
    assertEquals("/not-found", details.getUri());
  }

  @Test
  void extractErrorWithNoStatusCode() {
    when(request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE)).thenReturn(null);
    when(request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI)).thenReturn("/no-status");

    RequestDetails details = requestHandler.extractError(request);

    assertNull(details.getStatus());
    assertEquals("/no-status", details.getUri());
  }

  @Test
  void extractErrorWithNoUri() {
    when(request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE)).thenReturn(500);
    when(request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI)).thenReturn(null);

    RequestDetails details = requestHandler.extractError(request);

    assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, details.getStatus());
    assertNull(details.getUri());
  }

  @Test
  void extractErrorWithNoAttributes() {
    when(request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE)).thenReturn(null);
    when(request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI)).thenReturn(null);

    RequestDetails details = requestHandler.extractError(request);

    assertNull(details.getStatus());
    assertNull(details.getUri());
  }
}