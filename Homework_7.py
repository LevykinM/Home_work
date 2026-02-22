class Client:
    def __init__(self, name, age, sex, bill):
        self.name = name
        self.age = age
        self.sex = sex
        self.bill = bill

    def build_description(self):
        gender_map = {"male": "мужского", "female": "женского"}
        gender = gender_map.get(self.sex.lower(), "неизвестного")
        return f"Пользователь {self.name}, {self.age} лет, {gender} пола, совершил покупку на {self.bill} у.е."

class ClientLoader:
    def __init__(self,path):
        self.path = path
    def process(self,writer):
        count = 0
        with open(self.path,'r',encoding='utf-8') as f:
            next(f)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) < 6:
                    continue
                name = parts[0]
                sex = parts[3]
                try:
                    age = int(parts[4])
                    bill = int(parts[5])
                except ValueError:
                    continue
                client = Client(name, age, sex, bill)
                writer.write_one(client)
                count += 1
        return count

class DescriptionWriter:
    def __init__(self,path):
        self.path = path
    def open(self):
        self.file = open(self.path,'w',encoding='utf-8')
    def write_one(self,client):
        self.file.write(client.build_description()+'\n')
    def close(self):
        self.file.close()

class ClientPipeline:
    def __init__(self, input_path, output_path):
        self.loader = ClientLoader(input_path)
        self.writer = DescriptionWriter(output_path)
    def run(self):
        self.writer.open()
        try:
            count = self.loader.process(self.writer)
        finally:
            self.writer.close()
        print("Done", count, "clients")

pipeline = ClientPipeline("web_clients_correct.csv", "output.txt")
pipeline.run()