import React from 'react';

const CompanyList = ({ companies, selectedCompany, onCompanySelect, loading }) => {
  if (loading && companies.length === 0) {
    return (
      <div className="loading" style={{ height: '200px' }}>
        Loading companies...
      </div>
    );
  }

  return (
    <ul className="company-list">
      {companies.map((company) => (
        <li
          key={company.id}
          className={`company-item ${selectedCompany?.id === company.id ? 'active' : ''}`}
          onClick={() => onCompanySelect(company)}
        >
          <div className="company-symbol">{company.symbol}</div>
          <div className="company-name">{company.name}</div>
          <div className="company-sector">{company.sector}</div>
        </li>
      ))}
    </ul>
  );
};

export default CompanyList;
