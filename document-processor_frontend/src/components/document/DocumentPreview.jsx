import React from 'react';
import { Card, CardContent } from '@/components/ui/card';

const DocumentPreview = ({ url }) => {
  return (
    <Card>
      <CardContent className="p-2">
        <img
          src={url}
          alt="Document preview"
          className="max-h-96 mx-auto object-contain rounded"
        />
      </CardContent>
    </Card>
  );
};

export default DocumentPreview;
