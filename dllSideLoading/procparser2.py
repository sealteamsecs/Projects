import pandas as pd
from neo4j import GraphDatabase
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logging.info("Connected to Neo4j.")

    def close(self):
        self.driver.close()
        logging.info("Connection to Neo4j closed.")

    def import_data(self, chunk):
        with self.driver.session() as session:
            for _, row in chunk.iterrows():
                # Skip rows with NaN in crucial columns
                if pd.notna(row['Process Name']) and pd.notna(row['PID']) and pd.notna(row['Path']):
                    session.write_transaction(self.create_relationship, row)
                else:
                    logging.debug(f"Skipping row with missing data: {row}")

    @staticmethod
    def create_relationship(tx, row):
        query = """
        MERGE (p:Process {name: $process_name, pid: $pid})
        MERGE (path:Path {path: $path})
        MERGE (p)-[r:OPERATES {operation: $operation, result: $result}]->(path)
        """
        tx.run(query, process_name=row['Process Name'], pid=row['PID'],
               path=row['Path'], operation=row['Operation'], result=row['Result'])

def process_chunk(chunk, neo4j_importer):
    neo4j_importer.import_data(chunk)

def main():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "CHANGE_ME"
    importer = Neo4jImporter(uri, user, password)

    csv_file = 'Logfile3.csv'
    chunk_size = 20000  # Adjust based on your system's memory and the actual data size

    executor = ThreadPoolExecutor(max_workers=4)  # Adjust number of workers based on your machine's capability
    with pd.read_csv(csv_file, chunksize=chunk_size) as reader:
        futures = []
        for chunk in tqdm(reader, desc="Processing CSV"):
            future = executor.submit(process_chunk, chunk, importer)
            futures.append(future)

        for future in tqdm(futures, desc="Completing database operations"):
            try:
                future.result()  # Wait for all futures to complete
            except Exception as e:
                logging.error(f"Error processing a chunk: {e}")

    importer.close()

if __name__ == "__main__":
    main()
