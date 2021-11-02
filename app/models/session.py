class Session:
    def __init__(self, id, title, description, user_id, created_date, website_url, screen_record_url, webcam_record_url, heatmap_url, calib_points, iris_points):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_date = created_date
        self.website_url = website_url
        self.screen_record_url = screen_record_url
        self.webcam_record_url = webcam_record_url
        self.heatmap_url = heatmap_url
        self.calib_points = calib_points
        self.iris_points = iris_points

    def to_dict(self):
        return {
            u'id': self.id,
            u'title': self.title,
            u'description': self.description,
            u'user_id': self.user_id,
            u'created_date': self.created_date,
            u'website_url': self.website_url,
            u'screen_record_url': self.screen_record_url,
            u'webcam_record_url': self.webcam_record_url,
            u'heatmap_url': self.heatmap_url,
            u'callib_points': self.calib_points,
            u'iris_points': self.iris_points
        }