package ml.knu.mlhandler.utils;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;

@Slf4j
@Component
public class ExternalRequestHandler {

  private final RestTemplate rest;

  public ExternalRequestHandler(RestTemplate rest) {
    this.rest = rest;
  }

  public <T, G> Optional<G> post(String url, T body, Class<G> convertTo) {
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    var request = new HttpEntity<>(body, headers);
    try {
      return Optional.ofNullable(rest.postForObject(url, request, convertTo));
    } catch (Exception e) {
      log.warn(e.getMessage());
      return Optional.empty();
    }
  }

  public <G> Optional<G> get(String url, Class<G> convertTo) {
    try {
      return Optional.ofNullable(rest.getForObject(url, convertTo));
    } catch (Exception e) {
      log.warn(e.getMessage());
      return Optional.empty();
    }
  }
}
