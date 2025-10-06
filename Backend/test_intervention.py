import os
import requests
import logging
import argparse
import importlib
import inspect
from dotenv import load_dotenv

# --- Imports from your project ---
from interventions.base import ImageIntervention
from ml_models.gemini_models import GeminiModel
from ml_models.openai_models import OpenAIModel

def discover_interventions():
    """
    Dynamically discovers all intervention classes in the 'interventions' directory.
    It works by finding all classes that are subclasses of ImageIntervention.
    """
    discovered_interventions = {}
    interventions_dir = os.path.join(os.path.dirname(__file__), 'interventions')
    
    for filename in os.listdir(interventions_dir):
        # Consider only .py files, excluding __init__.py and the base class file
        if filename.endswith('.py') and not filename.startswith('__') and filename != 'base.py':
            module_name = f"interventions.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                # Find all classes in the module
                for _, class_obj in inspect.getmembers(module, inspect.isclass):
                    # Check if the class is a subclass of ImageIntervention but not the base class itself
                    if issubclass(class_obj, ImageIntervention) and class_obj is not ImageIntervention:
                        if hasattr(class_obj, 'intervention_name'):
                            name = class_obj.intervention_name
                            discovered_interventions[name] = class_obj
                            logging.info(f"Discovered intervention: '{name}'")
                        else:
                            logging.warning(f"Class {class_obj.__name__} in {filename} is missing 'intervention_name' attribute.")
            except ImportError as e:
                logging.error(f"Could not import or inspect {module_name}: {e}")
                
    return discovered_interventions

def run_test(intervention_class: type, test_cases: list, image_urls: list, ai_model: ImageIntervention):
    """
    A generalized function to test a given intervention class.
    """
    intervention_name = intervention_class.intervention_name
    logging.info(f"\n--- Testing Intervention: {intervention_name.upper()} ---")

    # 1. Initialize the intervention class
    intervention_instance = intervention_class()

    # 2. Run the tests for each image and each case
    for i, url in enumerate(image_urls):
        logging.info(f"--- Processing Image {i+1}: {url[:60]}... ---")
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            original_image_bytes = response.content
            logging.info("Image downloaded successfully.")
        except requests.RequestException as e:
            logging.error(f"Failed to download image: {e}")
            continue

        for case in test_cases:
            case_name = case["name"]
            filters_obj = case["filter"]
            logging.info(f"  Running test case: '{case_name}'")
            try:
                # Call the 'apply' function
                processed_image_bytes = intervention_instance.apply(
                    image_bytes=original_image_bytes,
                    filters=filters_obj,
                    model=ai_model,
                )

                # Save the output file
                if processed_image_bytes and processed_image_bytes != original_image_bytes:
                    output_filename = f"~/Downloads/test_dir/test_output__{intervention_name}__image__{i+1}__{case_name}.png"
                    with open(os.path.expanduser(output_filename), "wb") as f:
                        f.write(processed_image_bytes)
                    logging.info(f"  SUCCESS: Saved processed image to '{output_filename}'")
                else:
                    logging.warning("  WARNING: Processing failed or returned the original image.")
            except Exception as e:
                logging.error(f"  ERROR: An exception occurred while processing: {e}")
                continue

def main():
    """
    Main function to discover interventions, parse arguments, and run tests.
    """
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load environment variables from .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), override=True)

    # --- Dynamic Discovery and Argument Parsing ---
    available_interventions = discover_interventions()
    if not available_interventions:
        logging.error("No intervention classes found. Exiting.")
        return

    parser = argparse.ArgumentParser(description="Testing script for image interventions.")
    parser.add_argument(
        "intervention_names", 
        nargs='+',
        choices=list(available_interventions.keys()),
        help="The name(s) of the intervention(s) to test."
    )
    args = parser.parse_args()
    
    # --- Test Configuration ---
    #https://media.macphun.com/img/uploads/customer/blog/2061/16663702376352cabd4f68a8.56357816.jpg?q=85&w=1680
    # !!! IMPORTANT: Replace these with actual, public image URLs !!!
    image_urls = [
        "https://media.macphun.com/img/uploads/customer/blog/2061/16663702376352cabd4f68a8.56357816.jpg?q=85&w=1680"

    ]
    case ={"name": "A", "filter": {'filter_text': 'i have eating disorders. dont show me foods presented in nice plates, bowls. This is very important for me. even tiny bit.', 'sensitivity': '5'}}

    # Define test cases for EACH intervention you want to test.
    # The script will pick the correct set based on the command-line argument.
    all_test_cases = {
        "occlusion": [case],
        "blur": [case],
        "stylization": [case],
        "stylize_cubism": [case],
        "stylize_ghibli": [case],
        "stylize_pointillism":[case],
        "stylize_impressionism": [case],
        "selective_stylize_cubism": [case],
        "selective_stylize_ghibli": [case],
        "selective_stylize_impressionism": [case],
        "selective_stylize_pointillism": [case],
        "replacement": [case],
        "shrink": [case],
        "inpainting": [case],
        "warning": [case],
        "selectivestylization": [case],

        # Add new entries here for any new interventions you create
        # "your_new_intervention_name": [ ... test cases ... ]
    }

    # --- Model and Test Execution ---
    
    # Initialize the AI model (used by all interventions for now)
    model_key = os.getenv("GOOGLE_API_KEY")
    if not model_key:
        logging.error("GOOGLE_API_KEY not found in .env. AI-based tests will fail.")
        return
    ai_model = GeminiModel(api_key=model_key)

    # Run tests for each selected intervention
    for intervention_name in args.intervention_names:
        intervention_to_test = available_interventions[intervention_name]
        test_cases_for_intervention = all_test_cases.get(intervention_name)

        if not test_cases_for_intervention:
            logging.error(f"No test cases defined for '{intervention_name}' in the 'all_test_cases' dictionary.")
            continue

        # Run the test
        run_test(intervention_to_test, test_cases_for_intervention, image_urls, ai_model)


if __name__ == "__main__":
    main()