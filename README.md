# Auto Citation Generator

## Overview

The **Auto Citation Generator** is a Python-based automation script that classifies a given piece of text into predefined categories using a chatbot interface. It also generates relevant Google search queries based on the classification result. This project utilizes Selenium for web automation and is designed to streamline the process of text analysis and research.

## Features

- Classifies text into categories such as argumentative essay, narrative essay, expository essay, news article, blog post, or other.
- Generates Google search queries related to the classified text.
- Logs the filtered text, classification results, and generated search queries for reference.
- Handles common exceptions, ensuring smooth execution.

## Requirements

- Python 3.x
- Selenium
- Google Chrome
- ChromeDriver (compatible with your Chrome version)


### Command Line

```bash
python FindQueries.py "Your text here"
```

### Default Text

If no command-line argument is provided, the script will use the following default text:

```plaintext
In an age where climate change and environmental degradation are pressing concerns, the concept of sustainable living has gained significant traction...
```

## Logging

All output, including filtered text, classification results, and generated search queries, will be logged in `./log/output.log`. Additionally, the generated Google search queries will be saved in `search_queries.txt`.

## Error Handling

The script includes error handling for situations such as:
- Missing elements on the webpage.
- Timeout exceptions when waiting for elements.
- Stale element references during interaction.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for suggestions or improvements.

## Acknowledgements

- [Selenium](https://www.selenium.dev/) for web automation.
- [Python](https://www.python.org/) for programming.

### Customization
- Replace `aijcoder` in the clone command with your actual GitHub username or organization.
- Add more specific information regarding how to handle errors, improve the logging mechanism, or any other details unique to your implementation.
