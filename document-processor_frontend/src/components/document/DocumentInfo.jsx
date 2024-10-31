import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const DocumentInfo = ({ info }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Extracted Information</CardTitle>
      </CardHeader>
      <CardContent>
        <dl className="grid grid-cols-1 gap-4">
          <div>
            <dt className="text-sm font-medium text-gray-500">Name</dt>
            <dd className="mt-1 text-lg">{info.name || 'Not found'}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Document Number</dt>
            <dd className="mt-1 text-lg">{info.document_number || 'Not found'}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Expiration Date</dt>
            <dd className="mt-1 text-lg">{info.expiration_date || 'Not found'}</dd>
          </div>
        </dl>
      </CardContent>
    </Card>
  );
};

export default DocumentInfo;