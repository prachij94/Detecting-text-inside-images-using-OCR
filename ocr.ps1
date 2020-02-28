
param([Parameter(Mandatory=$true)][string]$url)

$cred = gcloud auth application-default print-access-token
$headers = @{ Authorization = "Bearer $cred" }


$url = "'"+ $url + "'"

$response = Invoke-WebRequest `
  -Method Post `
  -Headers $headers `
  -ContentType: "application/json; charset=utf-8" `
  -Body "{
      'requests': [
        {
          'image': {
            'source': {
              'imageUri': $url
            }
          },
          'features': [
            {
              'type': 'TEXT_DETECTION'
            }
          ]
        }
      ]
    }" `
  -Uri "https://vision.googleapis.com/v1/images:annotate" | Select-Object -Expand Content


  $x = $response | ConvertFrom-Json 

  $extractedtext = $x.responses.fullTextAnnotation.text
  $extractedtext

  


  $output1 = @(

  [pscustomobject]@{

  url = $url

  extractedtext  = $extractedtext


  }
  )
