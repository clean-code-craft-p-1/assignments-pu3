import sys
import requests

# Replace with your GitHub personal access token
GITHUB_TOKEN = ""

# Replace with your repository details
OWNER = "clean-code-craft-p-1"
REPO_NAME = "assignments-pu2"

# GraphQL endpoint
GITHUB_API_URL = "https://api.github.com/graphql"

# GraphQL mutation to create a discussion
CREATE_DISCUSSION_MUTATION = """
mutation($repositoryId: ID!, $title: String!, $body: String!, $categoryId: ID!) {
    createDiscussion(input: {repositoryId: $repositoryId, title: $title, body: $body, categoryId: $categoryId}) {
        discussion {
            id
            title
            url
        }
    }
}
"""

def get_repository_id(owner, repo_name):
        query = """
        query($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                id
            }
        }
        """
        variables = {"owner": owner, "name": repo_name}
        response = requests.post(
                GITHUB_API_URL,
                json={"query": query, "variables": variables},
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
        response_data = response.json()
        return response_data["data"]["repository"]["id"]

def get_category_id(repository_id, category_name):
        query = """
        query($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                discussionCategories(first: 10) {
                    nodes {
                        id
                        name
                    }
                }
            }
        }
        """
        variables = {"owner": OWNER, "name": REPO_NAME}
        response = requests.post(
                GITHUB_API_URL,
                json={"query": query, "variables": variables},
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
        print('finding discussion category')
        response_data = response.json()
        print(response_data)
        categories = response_data["data"]["repository"]["discussionCategories"]["nodes"]
        for category in categories:
                if category["name"] == category_name:
                        return category["id"]
        raise ValueError(f"Category '{category_name}' not found")

def create_discussion(repository_id, title, body, category_id):
        variables = {
                "repositoryId": repository_id,
                "title": title,
                "body": body,
                "categoryId": category_id
        }
        response = requests.post(
                GITHUB_API_URL,
                json={"query": CREATE_DISCUSSION_MUTATION, "variables": variables},
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
        )
        response_data = response.json()
        return response_data["data"]["createDiscussion"]["discussion"]

if __name__ == "__main__":
        try:
                GITHUB_TOKEN = sys.argv[1]  # Get the token from command line argument
                
                # Replace with your discussion details
                discussion_title = "What slows you down?"
                discussion_body = "What makes legacy code hard to work with?"
                discussion_category = "Polls"  # Replace with the name of your category
                discussion_body += "\n\n**Choices:**\n- Lack of documentation\n- Poor code readability\n- Inconsistent coding standards\n- Insufficient testing\n- Other"

                # Fetch repository ID
                repo_id = get_repository_id(OWNER, REPO_NAME)
                print(f"Repository ID: {repo_id}")
                # Fetch category ID
                category_id = get_category_id(repo_id, discussion_category)
                print(f"Category ID: {category_id}")

                # Create discussion
                discussion = create_discussion(repo_id, discussion_title, discussion_body, category_id)
                print(f"Discussion created successfully: {discussion['title']} ({discussion['url']})")
        except Exception as e:
                print(f"Error: {e}")
