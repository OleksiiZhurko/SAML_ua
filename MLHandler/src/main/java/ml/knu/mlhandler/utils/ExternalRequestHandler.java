package ml.knu.mlhandler.utils;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;

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
    return Optional.ofNullable(rest.postForObject(url, request, convertTo));
  }

  public <T, G> Optional<G> get(String url, Class<G> convertTo) {
    return Optional.ofNullable(rest.getForObject(url, convertTo));
  }
}
