// File: src/pages/About.jsx
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';

const About = () => {
  return (
    <Card className="max-w-3xl mx-auto">
      <CardHeader>
        <CardTitle>About Document Processor</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="prose">
          <p>
            Document Processor is a tool that helps you extract information from 
            passport and driving license documents. Simply upload an image of your 
            document, and our system will automatically extract key details such as:
          </p>
          <ul>
            <li>Full Name</li>
            <li>Document Number</li>
            <li>Expiration Date</li>
          </ul>
          <p>
            We support PNG, JPG, and JPEG formats with a maximum file size of 16MB.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default About;