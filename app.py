<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Surat</title>

    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family: Arial, sans-serif;
        }

        body{
            background: linear-gradient(135deg,#0f172a,#1e3a8a,#38bdf8);
            color:white;
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            text-align:center;
        }

        .container{
            background: rgba(255,255,255,0.1);
            padding:40px;
            border-radius:15px;
            backdrop-filter: blur(10px);
            box-shadow:0 8px 20px rgba(0,0,0,0.3);
            max-width:600px;
        }

        h1{
            font-size:50px;
            margin-bottom:20px;
        }

        p{
            font-size:20px;
            margin-bottom:30px;
            line-height:1.6;
        }

        button{
            padding:12px 25px;
            border:none;
            border-radius:8px;
            background:#facc15;
            color:#111827;
            font-size:18px;
            cursor:pointer;
            transition:0.3s;
        }

        button:hover{
            background:#eab308;
            transform:scale(1.05);
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>🌆 Welcome to Surat</h1>

        <p>
            Surat is known as the Diamond City and Textile Hub of India.
            Explore its culture, food, and beautiful places.
        </p>

        <button onclick="welcomeMessage()">Explore Surat</button>
    </div>

    <script>
        function welcomeMessage(){
            alert("Welcome to Surat! ❤️ Have a wonderful journey.");
        }
    </script>

</body>
</html>
