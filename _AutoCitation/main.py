"""
A program made for making things easier.
"""
import subprocess
import os

class AutoCitation:
    def __init__(self, text_to_classify):
        self.text_to_classify = text_to_classify

    def find_search_queries(self):
        """Runs the search query classification script with the provided text."""
        print("Starting the classification process...")
        try:
            result = subprocess.run(
                ['python3', 'FindQueries.py', self.text_to_classify],
                cwd=os.path.join(os.getcwd(), '_AutoCitation'),
                capture_output=True,
                text=True,
                check=True
            )
            print("Classification successful.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Classification process failed:")
            print(e.stderr)

    def find_real_cites(self, limit=12):
        """Runs the citation finding script as a subprocess with an optional limit."""
        print("Finding real citations...")
        try:
            result = subprocess.run(
                ['python3', 'FindCites.py', str(limit)],
                cwd=os.path.join(os.getcwd(), '_AutoCitation'),
                capture_output=True,
                text=True,
                check=True
            )
            print("Real citation finding successful.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Real citation finding failed:")
            print(e.stderr)

    def cite_for_websites(self):
        """Runs the citation generation script."""
        print("Generating citations for websites...")
        try:
            result = subprocess.run(
                ['python3', 'FindCitation.py'],
                cwd=os.path.join(os.getcwd(), '_AutoCitation'),
                capture_output=True,
                text=True,
                check=True
            )
            print("Citations generated successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Citation generation failed:")
            print(e.stderr)

    def run_all(self,limit=12):
        """Automates the search query, citation generation, and real citation finding processes."""
        self.find_search_queries()
        self.find_real_cites(limit)
        self.cite_for_websites()


if __name__ == "__main__":
    TEXT_TO_CLASSIFY = """
    In an age where climate change and environmental degradation are pressing concerns, the concept of sustainable living has gained significant traction. Sustainable living refers to a lifestyle that aims to reduce an individual's or society's use of the Earth's natural resources and personal resources. The goal is to create a balance between ecological health, economic viability, and social equity.

    One of the primary reasons sustainable living is crucial is the alarming rate at which we consume resources. According to the Global Footprint Network, humanity's demand for ecological resources exceeds what the Earth can regenerate in a year, leading to a deficit that can only worsen over time. By adopting sustainable practices, individuals can help to mitigate this imbalance.
    """

    auto_citation = AutoCitation(TEXT_TO_CLASSIFY)
    auto_citation.run_all()
