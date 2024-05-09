package ml.knu.mlhandler.service;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.http.HttpServletRequest;
import ml.knu.mlhandler.dto.internal.RequestDetails;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

@Service
public class RequestHandler {

  public RequestDetails extract(HttpServletRequest request) {
    Object requestedUri = request.getRequestURI();
    return extract(null, requestedUri);
  }

  public RequestDetails extractError(HttpServletRequest request) {
    Object status = request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);
    Object requestedUri = request.getAttribute(RequestDispatcher.ERROR_REQUEST_URI);
    return extract(status, requestedUri);
  }

  private RequestDetails extract(Object status, Object requestedUri) {
    var builder = RequestDetails.builder();
    if (status != null) {
      int statusCode = Integer.parseInt(status.toString());
      builder.status(HttpStatus.valueOf(statusCode));
    }
    if (requestedUri != null) {
      builder.uri(requestedUri.toString());
    }

    return builder.build();
  }
}
