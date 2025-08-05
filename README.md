# 🌾 Kisan Mitra - Farmer's Friend

A comprehensive AI-powered digital platform designed to empower Indian farmers with smart agricultural solutions, market connectivity, and knowledge resources.

## 🚀 Features

### 1. **Fasal Salah (Crop Advisory)**
- AI-powered crop recommendations based on location, soil type, and market conditions
- Real-time market price analysis
- Seasonal crop planning with profitability insights
- Personalized farming advice

### 2. **Mandi Connect (Marketplace)**
- Direct farmer-to-buyer marketplace
- Real-time market prices from government mandis
- Produce listing and discovery
- Eliminate middlemen for better profits

### 3. **Paudha Rakshak (Plant Protection)**
- AI-powered plant disease detection using image upload
- Instant diagnosis with treatment solutions
- Organic and chemical treatment recommendations
- Preventive measures guide

### 4. **Resource Optimizer**
- Smart irrigation calculator
- Fertilizer recommendation guide
- Soil health monitoring
- Water and resource optimization

### 5. **Gyan Kendra (Knowledge Center)**
- Latest agricultural news and updates
- Government scheme information
- Real-time weather forecasts and alerts
- Community forum for farmer discussions

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI Integration**: Ready for Gemini API integration
- **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)
- **Deployment**: Docker-ready

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd kisan-mitra
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
kisan-mitra/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── fasal_salah.html  # Crop advisory
│   ├── mandi_connect.html # Marketplace
│   ├── paudha_rakshak.html # Disease detection
│   ├── resource_optimizer.html # Resource management
│   └── gyan_kendra.html  # Knowledge center
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # Main JavaScript
│   ├── images/           # Image assets
│   └── uploads/          # User uploads
└── venv/                 # Virtual environment
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### API Integration
To integrate with real AI services (Gemini API):

1. Get API credentials from Google AI Studio
2. Add API key to environment variables
3. Update the API endpoints in `app.py`

## 🎯 Usage Guide

### For Farmers

1. **Get Crop Recommendations**
   - Navigate to "Fasal Salah"
   - Fill in your location, soil type, and other details
   - Get AI-powered crop recommendations

2. **Sell Your Produce**
   - Go to "Mandi Connect"
   - List your produce with details
   - Connect directly with buyers

3. **Detect Plant Diseases**
   - Visit "Paudha Rakshak"
   - Upload photos of affected plants
   - Get instant diagnosis and treatment

4. **Optimize Resources**
   - Use "Resource Optimizer"
   - Calculate irrigation needs
   - Get fertilizer recommendations

5. **Stay Informed**
   - Check "Gyan Kendra"
   - Read latest news and schemes
   - Participate in community discussions

## 🔮 Future Enhancements

- **Mobile App**: Native Android/iOS applications
- **Voice Interface**: Multilingual voice commands
- **IoT Integration**: Sensor data integration
- **Blockchain**: Transparent supply chain tracking
- **Advanced AI**: More sophisticated crop and disease analysis
- **Weather API**: Real-time weather data integration
- **Payment Gateway**: Integrated payment solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Indian farmers for inspiration
- Government agricultural departments for data
- Open source community for tools and libraries
- Agricultural experts for domain knowledge

## 📞 Support

For support and queries:
- Email: support@kisanmitra.com
- Website: www.kisanmitra.com
- Community Forum: Available in the Gyan Kendra section

---

**Built with ❤️ for Indian Farmers**

*Empowering agriculture through technology* 