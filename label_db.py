import sqlite3

class LabelDB(object):
  def __init__(self):
    self.conn = sqlite3.connect('label.db')

  def create_if_required(self):
    # called once to create db
      c = self.conn.cursor()
      try:
        c.execute('''create table imgs (
                          id integer primary key autoincrement,
                          filename text
                     )''')
        c.execute('''create table labels (
                          img_id integer,
                          x integer,
                          y integer
                     )''')
      except sqlite3.OperationalError:
        # assume table already exists? clumsy...
        pass

  def get_labels(self, img):
    id = self._id_for_img(img)
    if id is None: return []
    c = self.conn.cursor()
    c.execute("""select l.x, l.y                                                                                                 
                 from labels l join imgs i on l.img_id = i.id                                                                                   
                 where i.filename=?""", (img,))
    return c.fetchall()

  def set_labels(self, img, labels):
    img_id = self._id_for_img(img)
    if img_id is None:
      img_id = self._create_row_for_img(img)
    else:
      self._delete_labels_for_img_id(img_id)
    self._add_rows_for_labels(img_id, labels)    
      
  def _id_for_img(self, img):
    c = self.conn.cursor()
    c.execute("select id from imgs where filename=?", (img,))
    id = c.fetchone()
    if id is None:
      return None
    else:
      return id[0]
  
  def _create_row_for_img(self, img):
    c = self.conn.cursor()
    c.execute("insert into imgs (filename) values (?)", (img,))
    self.conn.commit()
    return self._id_for_img(img)

  def _delete_labels_for_img_id(self, img_id):
    c = self.conn.cursor()
    c.execute("delete from labels where img_id=?", (img_id,))
    self.conn.commit()

  def _add_rows_for_labels(self, img_id, labels):
    c = self.conn.cursor()
    for x, y in labels:
      c.execute("insert into labels (img_id, x, y) values (?, ?, ?)", (img_id, x, y,))
    self.conn.commit()
    
if __name__ == "__main__":
  db = LabelDB()
  db.create_if_required()
  print(db.get_labels("foo.png"))
  db.set_labels("foo.png", [(3,1), (4,1), (5,9)])
  print(db.get_labels("foo.png"))  
   
                                  
