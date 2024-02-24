from CaesarSQLDB.caesarcrud import CaesarCRUD
class CaesarCreateTables:
    def __init__(self) -> None:
        self.hackathonfields = ("username","question_set_title","question","useranswered","answer","result","hintsused")



    def create(self,caesarcrud : CaesarCRUD):
        caesarcrud.create_table("questionhackid",self.hackathonfields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","INT NOT NULL"),
        "hackathon")