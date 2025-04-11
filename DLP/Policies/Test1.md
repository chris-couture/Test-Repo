# Policy: HR_PII_Protection

**Description:**  
Protects personally identifiable information (PII) handled by HR staff.

**Regex Match / Classifier:**  
- Custom InfoType: `HR_PII_Regex`
- Matches: `\b\d{3}-\d{2}-\d{4}\b` (US SSNs)

**Source Locations:**  
- Microsoft Exchange
- SharePoint
- Teams Chat

**Destination Restrictions:**  
- Blocks external sharing
- Allows internal sharing with alert

**Severity Level:** High

**Enforcement Mode:** Audit + Block after 7 days

**Linked Classifiers:**  
- US_SSN  
- Employee_ID

**Created On:** 2024-10-10  
**Last Modified:** 2025-04-10  
**Related Issues:** #32, #45

---

## Changelog

- `2025-04-10`: Updated regex to improve accuracy
- `2025-01-02`: Enabled blocking for Teams messages
- Couture - Changing version blha blah testing what a commit actually does.
