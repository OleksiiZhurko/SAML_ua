package ml.knu.mlhandler.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpEntity;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ExternalRequestHandlerTest {

  private static final String URL = "https://test.com/api/data";

  @Mock
  private RestTemplate restTemplate;

  @InjectMocks
  private ExternalRequestHandler externalRequestHandler;

  @Test
  void postWhenServiceReturnsObjectShouldReturnOptionalOfObject() {
    TestDTO requestBody = new TestDTO("data");
    TestDTO expectedResponse = new TestDTO("response");
    when(restTemplate.postForObject(eq(URL), any(HttpEntity.class), eq(TestDTO.class)))
        .thenReturn(expectedResponse);

    Optional<TestDTO> response = externalRequestHandler.post(URL, requestBody, TestDTO.class);

    assertTrue(response.isPresent());
    assertEquals(expectedResponse, response.get());
  }

  @Test
  void postWhenServiceReturnsNullShouldReturnEmptyOptional() {
    TestDTO requestBody = new TestDTO("data");
    when(restTemplate.postForObject(eq(URL), any(HttpEntity.class), eq(TestDTO.class)))
        .thenReturn(null);

    Optional<TestDTO> response = externalRequestHandler.post(URL, requestBody, TestDTO.class);

    assertFalse(response.isPresent());
  }

  @Test
  void getWhenServiceReturnsObjectShouldReturnOptionalOfObject() {
    TestDTO expectedResponse = new TestDTO("value");
    when(restTemplate.getForObject(URL, TestDTO.class)).thenReturn(expectedResponse);

    Optional<TestDTO> response = externalRequestHandler.get(URL, TestDTO.class);

    assertTrue(response.isPresent());
    assertEquals(expectedResponse, response.get());
  }

  @Test
  void getWhenServiceReturnsNullShouldReturnEmptyOptional() {
    when(restTemplate.getForObject(URL, TestDTO.class)).thenReturn(null);

    Optional<TestDTO> response = externalRequestHandler.get(URL, TestDTO.class);

    assertFalse(response.isPresent());
  }

  static class TestDTO {
    String content;

    public TestDTO(String content) {
      this.content = content;
    }
  }
}