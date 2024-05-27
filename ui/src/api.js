const API_URL = 'http://localhost:8080/graphql';

export async function fetchGraphQL(query, variables = {}) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query, variables})
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
}

export const processTextsQuery = `
  query ProcessTexts($input: ProcessTextsInput!) {
    processTexts(input: $input) {
      model
      text
      predicted
      probabilities {
        positive
        neutral
        negative
      }
    }
  }
`;

export const modelsQuery = `
  query {
    models {
      name
      description
    }
  }
`;
